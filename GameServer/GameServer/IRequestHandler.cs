using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    struct RequestInfo
    {
        public int requestCode;
        public List<byte> buffer;
    }
    struct RequestResult
    {
        public List<byte> response;
    }
    internal interface IRequestHandler
    {
        bool isRequestRelevant(RequestInfo requestInfo);
        RequestResult handleRequest(RequestInfo requestInfo);
        void handleDisconnect();
    }
}
