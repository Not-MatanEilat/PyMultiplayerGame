using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class GameRequestHandler : IRequestHandler
    {
        private Game game;
        public GameRequestHandler(Game game)
        {
            this.game = game;
        }
        public bool IsRequestRelevant(RequestInfo requestInfo)
        {
            return requestInfo.requestCode == (int)RequestCodes.Move;
        }

        public RequestResult HandleRequest(RequestInfo requestInfo)
        {
            RequestResult requestResult = new RequestResult();
            requestResult.response = BytesHelper.StringToBytes("Hello, client!");
            return requestResult;
        }

        public void HandleDisconnect()
        {

        }
    }
}
