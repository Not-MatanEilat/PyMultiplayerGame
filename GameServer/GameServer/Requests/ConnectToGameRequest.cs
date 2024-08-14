using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Requests
{
    internal class ConnectToGameRequest : IRequest
    {
        private string name;

        public ConnectToGameRequest(int id, string name) : base(id)
        {
            this.name = name;
        }

        public string GetName()
        {
            return name;
        }
    }
}
