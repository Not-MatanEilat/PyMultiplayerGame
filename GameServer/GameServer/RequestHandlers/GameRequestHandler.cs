using GameServer.Exceptions;
using GameServer.GameRelated;
using GameServer.Helpers;
using GameServer.Requests;
using GameServer.Responses;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.RequestHandlers
{
    internal class GameRequestHandler : IRequestHandler
    {
        private const float maxDistanceDifferenceFromClientToServer = 150f;
        private Game game;
        private Player player;
        public GameRequestHandler(Game game, Player player)
        {
            this.game = game;
            this.player = player;
        }
        public bool IsRequestRelevant(RequestInfo requestInfo)
        {
            return requestInfo.requestCode == (int)RequestCodes.Move;
        }

        public RequestResult HandleRequest(RequestInfo requestInfo)
        {
            RequestResult result;
            try
            {
                switch (requestInfo.requestCode)
                {
                    case (int)RequestCodes.Move:
                        result = Move(requestInfo);
                        break;
                    default:
                        throw new GameException("Invalid request code");
                }


            }
            catch (GameException e)
            {
                ErrorResponse errorResponse = new ErrorResponse(requestInfo.requestCode, e.Message);
                Console.WriteLine("Error: " + e.Message);
                result.responseCode = requestInfo.requestCode;
                result.response = JsonResponseSerializer.serializeResponse(errorResponse);
                result.newHandler = this;
            }

            return result;
        }

        private RequestResult Move(RequestInfo requestInfo)
        {
            MoveRequest request = JsonRequestDeserializer.DeserializeRequest<MoveRequest>(requestInfo.buffer);
            if (Vector2.Distance(player.GetPosition(), request.GetPosition()) > maxDistanceDifferenceFromClientToServer)
            {
                throw new GameException("Can't let you move that far, buddy");
            }

            Console.WriteLine("Player moved to: " + request.GetPosition().X + " " + request.GetPosition().Y);

            player.SetPosition(request.GetPosition());

            RequestResult result = new RequestResult();
            result.responseCode = requestInfo.requestCode;
            result.response = JsonResponseSerializer.serializeResponse(new MoveResponse(requestInfo.requestCode, player.GetPosition()));
            result.newHandler = this;

            return result;
        }

        public void HandleDisconnect()
        {
            game.RemovePlayer(player);
        }
    }
}
