using System;
using System.Runtime.Serialization;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;

namespace DCEP.Node
{
    [DataContract]
    [KnownType(typeof(RandomPrimitiveEventGenerationService))]
    public abstract class PrimitiveEventSourceService
    {
        public INodeProxyProvider proxyProvider {get; set;}

        private readonly NodeName _nodeName;

        protected PrimitiveEventSourceService(INodeProxyProvider proxyProvider, NodeName nodeName)
        {
            this.proxyProvider = proxyProvider;
            _nodeName = nodeName;
        }

        protected void registerPrimitiveEvent(PrimitiveEvent e)
        {
            e.knownToNodes.Add(this._nodeName);
            proxyProvider.getProxy(_nodeName).RegisterPrimitiveEventInputFork(e);
        }

        public abstract void start();

        public abstract void stop();
    }
}