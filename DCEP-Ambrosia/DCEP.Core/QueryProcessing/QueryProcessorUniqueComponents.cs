using System.Diagnostics;
using System.Collections.Immutable;
using System.Collections;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using DCEP.Core;
using DCEP.Core.QueryProcessing;
using DCEP.Core.Utils;
using DCEP.Core.QueryProcessing.Constraints;
using DCEP.Core.Utils.LeastCommonAncestor;
using DCEP.Core.QueryProcessing.Operators;

namespace DCEP.Core
{
    [DataContract]
    public class QueryProcessorUniqueComponents : QueryProcessor
    {
        [DataMember]
        List<State> startStates;

        [DataMember]
        Dictionary<EventType, List<Activation>> activationsByInputEventType;

        [DataMember]
        ImmutableList<EventType> queryComponentNames;

        [DataMember]
        private LeastCommonAncestorFinder<QueryComponent> leastCommonAncestorFinder;

        [DataMember]
        private readonly List<PrimitiveBufferComponentAllMatchConstraint> pBCAllMatchConstraints;
        public QueryProcessorUniqueComponents(Query query, TimeSpan timeWindow) : base(query, timeWindow)
        {
            startStates = new List<State>();
            activationsByInputEventType = new Dictionary<EventType, List<Activation>>();

            leastCommonAncestorFinder = new LeastCommonAncestorFinder<QueryComponent>(query.rootOperator);

            this.pBCAllMatchConstraints = new List<PrimitiveBufferComponentAllMatchConstraint>(){
                    new WithinTimeWindowConstraint(timeWindow)
                };


            initialize();
        }

        private void initialize()
        {
            queryComponentNames = query.rootOperator.getComponentsAsEventTypes().ToImmutableList();

            startStates = createAutomata(new HashSet<EventType>(query.inputEvents), Enumerable.Empty<EventType>());

            foreach (var startState in startStates)
            {
                activationsByInputEventType[startState.requiredEventType] = new List<Activation>() { new Activation(startState) };
            }

        }

        private List<State> createAutomata(HashSet<EventType> remainingInputs, IEnumerable<EventType> preceedingEventTypes)
        {
            if (remainingInputs.Count == 0)
            {
                return null;
            }
            else
            {
                var result = new List<State>();

                foreach (var inputEvent in remainingInputs)
                {
                    // create state with constraints
                    var pBCAnyMatchConstraints = createPBCAnyMatchConstraints(inputEvent, preceedingEventTypes);

                    var bufferConstraints = new List<BufferConstraint>();
                    State s = new State(inputEvent, bufferConstraints, pBCAnyMatchConstraints, this.pBCAllMatchConstraints);

                    // create proceeding states
                    var newRemaining = new HashSet<EventType>(remainingInputs);
                    newRemaining.Remove(inputEvent);

                    var updatedPreceedingEventTypesList = preceedingEventTypes.ToList();
                    updatedPreceedingEventTypesList.Add(inputEvent);

                    s.nextStates = createAutomata(newRemaining, updatedPreceedingEventTypesList);

                    result.Add(s);
                }

                return result;
            }
        }

        internal List<PrimitiveBufferComponentAnyMatchConstraint> createPBCAnyMatchConstraints(EventType inputEvent, IEnumerable<EventType> preceedingEventTypes)
        {
            var output = new List<PrimitiveBufferComponentAnyMatchConstraint>();
            var equalIDGuaranteed = new HashSet<EventType>();

            foreach (var eventInBuffer in preceedingEventTypes)
            {
                // possibly deconstruct complex event types to primitive types for checking their respective constraints
                foreach (var primitiveInputEvent in inputEvent.parseToQueryComponent().getListOfPrimitiveEventTypes())
                {
                    foreach (var primitveEventInBuffer in eventInBuffer.parseToQueryComponent().getListOfPrimitiveEventTypes())
                    {
                        if (primitiveInputEvent.Equals(primitveEventInBuffer))
                        {
                            if (!equalIDGuaranteed.Contains(primitiveInputEvent))
                            {
                                output.Add(new EqualIDWhenEqualEventTypeConstraint(primitiveInputEvent));
                                equalIDGuaranteed.Add(primitiveInputEvent);
                            }

                            continue;
                        }

                        var op = (AbstractQueryOperator)leastCommonAncestorFinder.FindCommonParent(primitiveInputEvent, primitveEventInBuffer);

                        if (op is SEQOperator)
                        {
                            // derive predecessor or successor constraint

                            var first = op.getFirstOccuringChildOf(primitiveInputEvent, primitveEventInBuffer);

                            if (inputEvent.Equals(first))
                            {
                                output.Add(new SequenceConstraint(primitiveInputEvent, primitveEventInBuffer, SequenceType.IsPredecessor));
                            }
                            else if (primitveEventInBuffer.Equals(first))
                            {
                                output.Add(new SequenceConstraint(primitiveInputEvent, primitveEventInBuffer, SequenceType.IsSuccessor));
                            }
                        }

                    }
                }
            }

            return output;
        }

        public override IEnumerable<ComplexEvent> processInputEvent(AbstractEvent e)
        {
            if (!activationsByInputEventType.ContainsKey(e.type))
            {
                return Enumerable.Empty<ComplexEvent>();
            }

            List<ComplexEvent> outputEvents = new List<ComplexEvent>();

            foreach (var activation in activationsByInputEventType[e.type])
            {
                var (newactivations, outputeventcomponents) = activation.consumeEvent(e);

                if (newactivations != null)
                {
                    foreach (var newactivation in newactivations)
                    {
                        activationsByInputEventType[newactivation.currentState.requiredEventType].Add(newactivation);
                    }
                }

                if (outputeventcomponents != null)
                {
                    outputEvents.Add(new ComplexEvent(query.name, outputeventcomponents));
                }
            }

            return outputEvents;
        }
    }
}