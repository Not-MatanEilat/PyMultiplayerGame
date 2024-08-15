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

        public MoveRequest(int id, Vector2 position) : base(id)
        {
            this.position = position;
        }

        public Vector2 GetPosition()
        {
            return position;
        }
    }
}
