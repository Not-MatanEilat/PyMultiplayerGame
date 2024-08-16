using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Requests
{
    internal class MoveRequest : IRequest
    {
        private Vector2 position;
        private int requestId;

        public MoveRequest(int requestId, Vector2 position) : base()
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
