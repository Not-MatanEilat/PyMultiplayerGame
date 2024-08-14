using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Responses
{
    abstract class IResponse
    {
        private int id;

        public IResponse(int id)
        {
            this.id = id;
        }

        public int GetId()
        {
            return id;
        }
    }
}
