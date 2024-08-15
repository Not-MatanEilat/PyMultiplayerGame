using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GameServer.Helpers;

namespace GameServer.RequestHandlers
{
    internal class TestHandler : IRequestHandler
    {

        public bool IsRequestRelevant(RequestInfo requestInfo)
        {
            return true;
        }

        public RequestResult HandleRequest(RequestInfo requestInfo)
        {
            RequestResult requestResult = new RequestResult();
            requestResult.response = BytesHelper.StringToBytes("Hello, client!");
            return requestResult;
        }

        public void HandleDisconnect()
        {
            int x = 1;
        }
    }
}
