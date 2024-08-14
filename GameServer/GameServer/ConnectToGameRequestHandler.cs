using GameServer.Requests;
using GameServer.Responses;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class ConnectToGameRequestHandler : IRequestHandler
    {
        private Game game;
        public ConnectToGameRequestHandler(Game game)
        {
            this.game = game;
        }
        public bool IsRequestRelevant(RequestInfo requestInfo)
        {
            return requestInfo.requestCode == (int)RequestCodes.ConnectToGame;
        }

        public RequestResult HandleRequest(RequestInfo requestInfo)
        {
            ConnectToGameRequest request = JsonRequestDeserializer.DesrializeRequest(requestInfo.buffer);
            Console.WriteLine("Id request: " + request.GetId());
            Console.WriteLine("Name request: " + request.GetName());

            ConnectToGameResponse response = new ConnectToGameResponse(1, game.GetBlocks());

            RequestResult result = new RequestResult();

            result.responseCode = requestInfo.requestCode;
            result.response = JsonResponseSerializer.serializeResponse(response);

            return result;
        }

        public void HandleDisconnect()
        {

        }
    }
}
