using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Responses
{
    internal class MoveResponse : IResponse
    {
        private int requestId;
        private Vector2 position;

        public MoveResponse(int requestId, Vector2 position) : base()
        {
            this.position = position;
            this.requestId = requestId;
        }

        public Vector2 GetPosition()
        {
            return position;
        }

        public int GetRequestId()
        {
            return requestId;
        }
    }
}
