using GameServer.Exceptions;
using GameServer.GameRelated;
using GameServer.Helpers;
using GameServer.Requests;
using GameServer.Responses;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.RequestHandlers
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
            RequestResult result;

            try
            {
                result = Connect(requestInfo);
            }
            catch (GameException e)
            {
                ErrorResponse errorResponse = new ErrorResponse(e.Message);
                Console.WriteLine("Error: " + e.Message);
                result.responseCode = requestInfo.requestCode;
                result.response = JsonResponseSerializer.serializeResponse(errorResponse);
                result.newHandler = this;
            }
            return result;
        }

        private RequestResult Connect(RequestInfo requestInfo)
        {
            ConnectToGameRequest request = JsonRequestDeserializer.DeserializeRequest<ConnectToGameRequest>(requestInfo.buffer);
            Console.WriteLine("Name request: " + request.GetName());


            Player player = new Player(request.GetName(), game);
            game.AddPlayer(player);

            RequestResult result = new RequestResult();

            ConnectToGameResponse response = new ConnectToGameResponse(game.GetBlocks());
            result.response = JsonResponseSerializer.serializeResponse(response);

            result.responseCode = requestInfo.requestCode;

            result.newHandler = new GameRequestHandler(game, player);
            return result;
        }

        public void HandleDisconnect()
        {

        }
    }
}
