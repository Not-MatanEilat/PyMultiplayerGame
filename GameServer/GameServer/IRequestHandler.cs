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
        public int responseCode;
        public List<byte> response;
    }
    internal interface IRequestHandler
    {
        bool IsRequestRelevant(RequestInfo requestInfo);
        RequestResult HandleRequest(RequestInfo requestInfo);
        void HandleDisconnect();
    }
}
