using System;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Runtime.Serialization;
using System.Threading;
using DCEP.Core;
using DCEP.Core.Utils;

namespace DCEP.Node
{
    [DataContract]
    public class DatasetPrimitiveEventInputService : PrimitiveEventSourceService
    {
        [DataMember] private string TAG { get; set; }
        [DataMember] private readonly string _filePath;
        [DataMember] private readonly DCEPSettings _settings;
        
        [DataMember] private bool _continueRunning;
        
        [DataMember] private Stopwatch _stopwatch;
        [DataMember] private TimeSpan _offset;
        [DataMember] private string _eventtype;
        [DataMember] private bool _candidateInQueue;

        public DatasetPrimitiveEventInputService(INodeProxyProvider proxyProvider, string tag, string filePath,
            NodeName nodeName, DCEPSettings settings) : base(proxyProvider, nodeName)
        {
            TAG = tag + "[DatasetPrimitiveEventInputService] ";
            var inputfilepath = new FileInfo(settings.InputFilePath).Directory.FullName;
            filePath = filePath.Replace("%NodeName%", nodeName.ToString());
            _filePath = Path.Combine(inputfilepath, Path.GetFileName(filePath));
            _settings = settings;
        }

        public override void start()
        {
            _continueRunning = true;
            Thread t = new Thread(new ThreadStart(SeparateThreadMethod));
            t.Start();
        }

        private void SeparateThreadMethod()
        {
            _stopwatch = new Stopwatch();
            _stopwatch.Start();

            Console.WriteLine(TAG + "Starting to read dataset file "+_filePath);
            System.IO.StreamReader file =
                new System.IO.StreamReader(_filePath);

            _candidateInQueue = false;


            while (_continueRunning)
            {
                if (!_candidateInQueue)
                {
                    var line = file.ReadLine();

                    if (line == null)
                    {
                        Console.WriteLine(TAG + " Reached end of input file. Terminating primitive input service.");
                        return;
                    }

                    var timestampstring = line.Split(',')[0].Replace("\"", "");
                    //_offset = TimeSpan.ParseExact(timestampstring, _settings.datasetDateFormatString,
                    //    CultureInfo.InvariantCulture, TimeSpanStyles.None);
                    _offset = TimeSpan.Parse(timestampstring, CultureInfo.InvariantCulture);
                    _offset = _offset.Multiply(1.0/_settings.datasetSpeedup);
                    _eventtype = line.Split(',')[1].Replace("\"", "");
                    _candidateInQueue = true;
                }

                if (_offset < _stopwatch.Elapsed)
                {
                    registerPrimitiveEvent(new PrimitiveEvent(new EventType(_eventtype)));
                    _candidateInQueue = false;
                }
            }
        }

        public override void stop()
        {
            _continueRunning = false;
        }
    }
}