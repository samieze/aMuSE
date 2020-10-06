using System.Runtime.Serialization;

namespace DCEP.Node.Benchmarking
{
    [DataContract]
    public struct BenchmarkRecord
    {
        [DataMember]
        public double eventTimeLatency { get; set; }

        [DataMember]
        public double processingTimeLatency { get; set; }

        [DataMember]
        public double throughput { get; set; }
        
        [DataMember]
        public double processedComplexCount { get; set;  }
    }
}