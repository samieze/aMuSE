using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP.Core;

namespace DCEP.Core.QueryProcessing
{
    [DataContract]
    [KnownType(typeof(QueryProcessorUniqueComponents))]
    public abstract class QueryProcessor
    {
        [DataMember]
        public readonly Query query;

        [DataMember]
        protected readonly TimeSpan timeWindow;

        public abstract IEnumerable<ComplexEvent> processInputEvent(AbstractEvent e);

        protected QueryProcessor(Query query, TimeSpan timeWindow)
        {
            this.query = query;
            this.timeWindow = timeWindow;
        }

        public static QueryProcessor getQueryProcessorForQuery(Query q, TimeSpan timeWindow)
        {
            // check if any primitive events occure more than once in the query
            var primitiveEventTypesInQuery = q.rootOperator.getListOfPrimitiveEventTypes();
            var numberOfUniquePrimitiveEventTypesInQuery = new HashSet<EventType>(primitiveEventTypesInQuery).Count;

            if (primitiveEventTypesInQuery.Count == numberOfUniquePrimitiveEventTypesInQuery)
            {
                // no duplicate primitive events in query
                return new QueryProcessorUniqueComponents(q, timeWindow);
            }
            else
            {
                return null;
            }


        }
    }

}