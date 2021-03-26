using DCEP.Core;

namespace DCEP.Node
{
    public interface ICommunicationRelay
    {
        void sendEvent(AbstractEvent e, NodeName target);

    }
}