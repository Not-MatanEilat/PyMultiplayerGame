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
            return requestInfo.requestCode == (int)PacketsCodes.Move;
        }

        public RequestResult HandleRequest(RequestInfo requestInfo)
        {
            RequestResult result;
            try
            {
                switch (requestInfo.requestCode)
                {
                    case (int)PacketsCodes.Move:
                        result = Move(requestInfo);
                        break;
                    default:
                        throw new GameException("Invalid request code");
                }


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

        private RequestResult Move(RequestInfo requestInfo)
        {
            MoveRequest request = JsonRequestDeserializer.DeserializeRequest<MoveRequest>(requestInfo.buffer);
            MoveResponse moveResponse;

            // if the user is trying to move too far, we don't allow it
            if (Vector2.Distance(player.GetPosition(), request.GetPosition()) <= maxDistanceDifferenceFromClientToServer)
            {
                player.SetPosition(request.GetPosition());
                moveResponse = new MoveResponse(request.GetRequestId(), request.GetPosition());

            }
            else
            {
                moveResponse = new MoveResponse(request.GetRequestId(), player.GetPosition());
                moveResponse.SetOk(false);
            }

            RequestResult result = new RequestResult();
            result.responseCode = requestInfo.requestCode;
            result.response = JsonResponseSerializer.serializeResponse(moveResponse);
            result.newHandler = this;


            return result;
        }

        public void HandleDisconnect()
        {
            Console.WriteLine("Player disconnected");
            game.RemovePlayer(player);
        }
    }
}
