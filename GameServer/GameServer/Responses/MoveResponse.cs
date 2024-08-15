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
        Vector2 position;

        public MoveResponse(int id, Vector2 position) : base(id)
        {
            this.position = position;
        }

        public Vector2 GetPosition()
        {
            return position;
        }
    }
}
