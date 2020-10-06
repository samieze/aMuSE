using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core
{
    [DataContract]
    public class ComplexEvent : AbstractEvent
    {
        [DataMember]
        public IEnumerable<AbstractEvent> children { get; private set; }

        public ComplexEvent(EventType name, IEnumerable<AbstractEvent> outputeventcomponents) : base(name)
        {
            children = outputeventcomponents;
        }
    }
}