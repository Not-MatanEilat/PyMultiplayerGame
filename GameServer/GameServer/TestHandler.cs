using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class TestHandler : IRequestHandler
    {

        public bool isRequestRelevant(RequestInfo requestInfo)
        {
            return true;
        }

        public RequestResult handleRequest(RequestInfo requestInfo)
        {
            RequestResult requestResult = new RequestResult();
            requestResult.response = BytesHelper.StringToBytes("Hello, client!");
            return requestResult;
        }

        public void handleDisconnect()
        {
            int x = 1;
        }
    }
}
