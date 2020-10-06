using DCEP.Core;
using System;
using System.Runtime.Serialization;

namespace DCEP.Core
{
    [DataContract]
    public class PrimitiveEvent : AbstractEvent
    {
        public PrimitiveEvent(EventType name) : base(name)
        {
        }

        public PrimitiveEvent(string name) : base(new EventType(name))
        {

        }
    }
}