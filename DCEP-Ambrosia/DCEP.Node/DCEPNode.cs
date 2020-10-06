using System.Diagnostics;
using System;
using DCEP.Core.QueryProcessing;
using System.Runtime.Serialization;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using System.Collections.Concurrent;
using DCEP.Core;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core.Utils;
using DCEP.Node.Benchmarking;
using DCEP.Core.DCEPControlMessage;

namespace DCEP.Node
{
    [DataContract]
    public class DCEPNode : IAmbrosiaNode
    {
        [DataMember] NodeExecutionState state;
        [DataMember] private readonly SerializableQueue<AbstractEvent> externalEventQueue;
        [DataMember] private readonly SerializableQueue<AbstractEvent> internalEventQueue;
        [DataMember] private readonly SerializableQueue<DCEPControlMessage> controlMessageQueue;
        [DataMember] public Dictionary<EventType, ForwardRule> forwardRules { get; set; }
        [DataMember] private readonly DCEPSettings settings;
        [DataMember] private readonly string TAG;
        [DataMember] public long receivedEventCount { get; set; }
        [DataMember] public long locallyGeneratedComplexEventCount { get; set; }
        [DataMember] public long locallyGeneratedPrimitiveEventCount { get; set; }
        
        [DataMember] public long locallyDroppedComplexEvents { get; set; }
        [DataMember] public NodeName nodeName { get; set; }
        [DataMember] private List<QueryProcessor> queryProcessors;
        [DataMember] private ForwardRuleProcessor forwardRuleProcessor;
        [DataMember] private Random randomNumberGenerator = new Random(); // for the implementation of selection rates
        [DataMember] Stopwatch stopwatch = new Stopwatch(); // for performance benchmarking
        [DataMember] ExecutionPlan executionPlan;
        [DataMember] private readonly BenchmarkMeter benchmarkMeter;
        [DataMember] PrimitiveEventSourceService primitiveEventSourceService;
        [DataMember] private DirectorNodeService directorNodeService = null;
        //private Dictionary<NodeName, IAmbrosiaNodeProxy> proxyDict;
        //private IAmbrosiaNodeProxy directorNodeProxy { get; set; }
        //private IAmbrosiaNodeProxy thisProxy { get; set; }

        private INodeProxyProvider proxyProvider;
        [DataMember] long lastStatusMessageToCoordinator = -1;
        [DataMember] private bool sentReadyToStartMessage;
        [DataMember] private long _remainingTimeLastPrintTime = 0;
        [DataMember] private long _remainingTimeLastProcessedCount = 0;

        public DCEPNode(NodeName name, string[] inputlines, DCEPSettings settings)
        {
            TAG = "[" + name + "] ";
            Console.WriteLine(TAG + "DCEPNode Constructor called.");
            state = NodeExecutionState.WaitForStart;
            receivedEventCount = 0;
            sentReadyToStartMessage = false;
            nodeName = name;
            externalEventQueue = new SerializableQueue<AbstractEvent>();
            internalEventQueue = new SerializableQueue<AbstractEvent>();
            controlMessageQueue = new SerializableQueue<DCEPControlMessage>();
            queryProcessors = new List<QueryProcessor>();
            this.settings = settings;
            executionPlan = new ExecutionPlan(inputlines);
            benchmarkMeter = new BenchmarkMeter(settings, nodeName);
            createQueryProcessors(executionPlan.queriesByNodeName[nodeName]);
        }

        private void initPrimitiveEventSourceService()
        {
            switch (executionPlan.primitiveInputMode)
            {
                case PrimitiveInputMode.RANDOM_WITH_RATES:
                    primitiveEventSourceService =  new RandomPrimitiveEventGenerationService(nodeName,
                        executionPlan.networkPlan[nodeName],
                        proxyProvider,
                        settings);
                    break;
            
                case PrimitiveInputMode.DATASET:
                    primitiveEventSourceService = new DatasetPrimitiveEventInputService(proxyProvider,
                        TAG,
                        executionPlan.datasetFileNameTemplate,
                        nodeName,
                        settings);
                    break;
            
                default:
                    throw new ArgumentException("Unknown primitiveInputMode in executionPlan.");
            }
        }

        public void onFirstStart(INodeProxyProvider proxyProvider){
            this.proxyProvider = proxyProvider;

            /*proxyDict = new Dictionary<NodeName, IAmbrosiaNodeProxy>();
            
            foreach (var nName in executionPlan.networkPlan.Keys)
            {
                proxyDict[nName] = proxyProvider.getProxy(nName);
            }
            */
            if (settings.directorNodeName == null){
                throw new ArgumentException(TAG + "DirectorNodeName must not be null.");
            }

            /*if (proxyDict.Keys.Contains(settings.directorNodeName)){
                throw new ArgumentException(TAG + "DirectorNodeName " + settings.directorNodeName.ToString() + " could not be found in proxydict.");
            }*/

            //directorNodeProxy = proxyDict[settings.directorNodeName];
            //thisProxy = proxyDict[nodeName];
            
            var forwardRules = executionPlan.forwardRulesByNodeName[nodeName];
            this.forwardRuleProcessor = new ForwardRuleProcessor(TAG, forwardRules, proxyProvider);

            initPrimitiveEventSourceService();

            if (this.nodeName.Equals(settings.directorNodeName))
            {
                directorNodeService = new DirectorNodeService(TAG,
                                                              executionPlan.networkPlan.Keys.ToList(),
                                                              proxyProvider,
                                                              settings);
            }
      
            
        }

        public void threadStartMethod()
        {
            stopwatch.Start();

            while (true)
            {
                processControlMessages();

                switch (state)
                {
                    case NodeExecutionState.WaitForStart:
 /*                        // broadcast isready signal to directorNode every second
                        if (stopwatch.ElapsedMilliseconds - lastStatusMessageToCoordinator > 1000){
                            proxyProvider.getProxy(settings.directorNodeName).ReceiveDCEPControlMessageFork(new NodeIsReadyToStartMessage(nodeName));
                            //Console.WriteLine(TAG + "sending ready to start message to director node "+settings.directorNodeName.ToString());
                            lastStatusMessageToCoordinator = stopwatch.ElapsedMilliseconds;
                        } */

                        if (!sentReadyToStartMessage){
                            proxyProvider.getProxy(settings.directorNodeName).ReceiveDCEPControlMessageFork(new NodeIsReadyToStartMessage(nodeName));
                            sentReadyToStartMessage = true;
                        }

                    break;

                    case NodeExecutionState.DoStartInputGeneration:
                        // TODO: check if this is not already running and throw an error if it is
                        primitiveEventSourceService.start();
                        state = NodeExecutionState.Running;
                        processingStep();
                    break;

                    case NodeExecutionState.Running:
                        processingStep();
                    break;

                    case NodeExecutionState.DoStopInputGeneration:
                        primitiveEventSourceService.stop();
                        state = NodeExecutionState.ProcessingRemainder;

                    break;

                    case NodeExecutionState.ProcessingRemainder:
                        processingStep();
                        
                        // when queues are empty, send isReadyToTerminate message every second 
                        if (getQueuedEventCount() == 0)
                        {
                            if (stopwatch.ElapsedMilliseconds - lastStatusMessageToCoordinator > 1000)
                            {
                                proxyProvider.getProxy(settings.directorNodeName)
                                    .ReceiveDCEPControlMessageFork(new NodeIsReadyToTerminateMessage(nodeName));
                                lastStatusMessageToCoordinator = stopwatch.ElapsedMilliseconds;
                            }
                        }

                        break;

                    case NodeExecutionState.DoSendExperimentDataAndTerminate:

                        var data = new ExperimentRunData(
                            locallyGeneratedComplexEventCount,
                            receivedEventCount,
                            locallyGeneratedPrimitiveEventCount,
                            locallyDroppedComplexEvents);

                        proxyProvider.getProxy(settings.directorNodeName).ReceiveDCEPControlMessageFork(new ExperimentRunNodeDataMessage(nodeName, data));
                        Console.WriteLine(TAG + "Sent experiment data. Update loop is terminating.");
                        Thread.Sleep(500);
                        if (getQueuedEventCount() > 0)
                        {
                            Console.WriteLine(TAG + String.Format("WARNING: requested to terminate with {0} events left in queue.", getQueuedEventCount()));
                        }

                        if (directorNodeService != null){
                            while(!directorNodeService.localNodeCanTerminate){
                                processControlMessages();
                            }
                        }
                        return;



                    case NodeExecutionState.DoTerminate:
                        if (getQueuedEventCount() > 0){
                            Console.WriteLine(TAG + String.Format("WARNING: requested to terminate with {0} events left in queue.", getQueuedEventCount()));
                        }
                        return;
                }

            }
        }

        public long getQueuedEventCount()
        {
            return internalEventQueue.Data.LongCount() + externalEventQueue.Data.LongCount();
        }

        private void createQueryProcessors(IEnumerable<Query> queries)
        {
            var timeWindow = settings.timeUnit.GetTimeSpanFromDuration(settings.timeWindow);
            timeWindow = timeWindow.Multiply(1.0 / settings.datasetSpeedup);
            
            foreach (var q in queries)
            {
                var processor = QueryProcessor.getQueryProcessorForQuery(q, timeWindow);
                if (processor != null)
                {
                    queryProcessors.Add(processor);
                }
                else
                {
                    Console.WriteLine(TAG + String.Format("!WARNING! - Inactive Query '{0}' due not no matching QueryProcessor implementation.", q.ToString()));
                }
            }
        }

        public void processControlMessages(){
            while(!controlMessageQueue.Data.IsEmpty){
                DCEPControlMessage controlMessage = null;
                if (controlMessageQueue.Data.TryDequeue(out controlMessage)){

                    if (controlMessage is NodeInfoForCoordinatorMessage){
                        directorNodeService.ProcessNodeInfoForCoordinatorMessage(controlMessage as NodeInfoForCoordinatorMessage);

                    } else if (controlMessage is UpdatedExecutionStateMessage){
                        var newState = (controlMessage as UpdatedExecutionStateMessage).newState;
                        Console.WriteLine(TAG + "updated execution state from " + state.ToString() + " to "+newState.ToString());
                        state = newState;
                    }
                }
            }
        }

        public async Task<int> ReceiveDCEPControlMessageAsync(DCEPControlMessage controlMessage)
        {
            controlMessageQueue.Data.Enqueue(controlMessage);
            return 0;
        }

        public async Task<int> ReceiveExternalEventAsync(AbstractEvent e)
        {
            receivedEventCount++;
            externalEventQueue.Data.Enqueue(e);

            return 0;
        }

        public void processingStep(){

            AbstractEvent externalEvent = null;
            if (externalEventQueue.Data.TryDequeue(out externalEvent))
            {
                var processingStart = stopwatch.ElapsedMilliseconds;

                externalEvent.knownToNodes.Add(this.nodeName);
                processQueries(externalEvent);

                benchmarkMeter.registerProcessedEvent(externalEvent, processingStart, stopwatch.ElapsedMilliseconds);
            }

            AbstractEvent internalEvent = null;
            if (internalEventQueue.Data.TryDequeue(out internalEvent))
            {
                var processingStart = stopwatch.ElapsedMilliseconds;

                processQueries(internalEvent);
                forwardRuleProcessor.processEvent(internalEvent);

                benchmarkMeter.registerProcessedEvent(internalEvent, processingStart, stopwatch.ElapsedMilliseconds);
            }

            benchmarkMeter.tick(stopwatch.ElapsedMilliseconds);
            updateRemainingTimePrinter(stopwatch.ElapsedMilliseconds);
        }

        private void processQueries(AbstractEvent inputEvent)
        {
            foreach (var queryProcessor in queryProcessors)
            {
                foreach (var outputEvent in queryProcessor.processInputEvent(inputEvent))
                {
                    if (queryProcessor.query.selectionRate != 1.0d)
                    {
                        var doDropIt = randomNumberGenerator.NextDouble() > queryProcessor.query.selectionRate;
                        proxyProvider.getProxy(nodeName).RegisterComplexEventMatchFork(outputEvent, doDropIt);
                    }
                    else
                    {
                        proxyProvider.getProxy(nodeName).RegisterComplexEventMatchFork(outputEvent, false);
                    }
                }
            }
        }

        public async Task RegisterPrimitiveEventInputAsync(PrimitiveEvent e) {
            Console.WriteLine(TAG + String.Format("Generated primitive event {0}.", e));

            locallyGeneratedPrimitiveEventCount++;
            internalEventQueue.Data.Enqueue(e);
        }

        public async Task RegisterComplexEventMatchAsync(ComplexEvent e, bool isDropped)
        {
            benchmarkMeter.registerNewComplexEvent(e);
            if (!isDropped)
            {
                locallyGeneratedComplexEventCount++;
                internalEventQueue.Data.Enqueue(e);
            }
            else
            {
                locallyDroppedComplexEvents++;
            }
        }

        public void  terminateImmediately(){
            state = NodeExecutionState.DoTerminate;
            if (directorNodeService != null){
                directorNodeService.terminateAllNodesImmediately();
            }
        }
        public void updateRemainingTimePrinter(long passedMilliseconds)
        {
            if (_remainingTimeLastPrintTime == 0)
            {
                _remainingTimeLastPrintTime = passedMilliseconds;
                return;
            }
            
            // after 60 seconds, every 60 seconds: 
            if (passedMilliseconds - _remainingTimeLastPrintTime > 60000)
            {
                var totalEvents = locallyGeneratedComplexEventCount +
                                  receivedEventCount +
                                  locallyGeneratedPrimitiveEventCount;

                var throughput = totalEvents - _remainingTimeLastProcessedCount;
                if (throughput == 0) return;
                
                double interval = (passedMilliseconds - _remainingTimeLastPrintTime);
                double queueCount = getQueuedEventCount();
                double estimatedMs  = interval * (queueCount / throughput);
                long estimatedMinutes = (long) (estimatedMs / 60000);
                
                _remainingTimeLastPrintTime = passedMilliseconds;
                _remainingTimeLastProcessedCount = totalEvents;
                Console.WriteLine(TAG + $"Estimated time for processing queued events: {estimatedMinutes} minutes ({queueCount} events in queue) ");
            }
        }
    }
}
