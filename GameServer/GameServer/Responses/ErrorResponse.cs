using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Responses
{
    internal class ErrorResponse : IResponse
    {
        private string message;

        public ErrorResponse(int id, string message) : base(id)
        {
            this.message = message;
        }

        public string GetMessage()
        {
            return message;
        }
    }
}
