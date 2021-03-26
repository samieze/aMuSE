using DCEP.Core;

namespace DCEP.Node
{
    public interface INodeProxyProvider
    {
        IAmbrosiaNodeProxy getProxy(NodeName nodeName);
    }
}