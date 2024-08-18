using GameServer.GameRelated;
using GameServer.Responses;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Helpers
{
    internal class JsonResponseSerializer
    {
        public static List<byte> serializeResponse(ConnectToGameResponse response)
        {
            JObject json = new JObject();
            json["ok"] = response.IsOk();

            JArray blocksArray = new JArray();
            foreach (RectangleF block in response.GetBlocks())
            {
                JObject blockObject = new JObject();
                blockObject["x"] = block.X;
                blockObject["y"] = block.Y;
                blockObject["width"] = block.Width;
                blockObject["height"] = block.Height;
                blocksArray.Add(blockObject);
            }
            json["blocks"] = blocksArray;
            List<Player> players = response.GetPlayers();
            JArray playersArray = new JArray();
            foreach (Player player in players)
            {
                JObject playerObject = new JObject();
                playerObject["name"] = player.GetName();
                playerObject["position"] = JObject.FromObject(new { x = player.GetPosition().X, y = player.GetPosition().Y });
                playersArray.Add(playerObject);
            }
            json["players"] = playersArray;


            return GetBufferFromJson(json);
        }

        public static List<byte> serializeResponse(MoveResponse response)
        {
            JObject json = new JObject();
            json["request_id"] = response.GetRequestId();
            json["ok"] = response.IsOk();
            json["position"] = JObject.FromObject(new { x = response.GetPosition().X, y = response.GetPosition().Y });

            return GetBufferFromJson(json);

        }

        public static List<byte> serializeResponse(ConnectedToServerResponse response)
        {
            JObject json = new JObject();
            json["ok"] = response.IsOk();

            return GetBufferFromJson(json);

        }

        public static List<byte> serializeResponse(UpdatePlayersResponse response)
        {
            JObject json = new JObject();
            json["ok"] = response.IsOk();
            List<Player> players = response.GetPlayers();
            JArray playersArray = new JArray();
            foreach (Player player in players)
            {
                JObject playerObject = new JObject();
                playerObject["name"] = player.GetName();
                playerObject["position"] = JObject.FromObject(new { x = player.GetPosition().X, y = player.GetPosition().Y });
                playersArray.Add(playerObject);
            }
            json["players"] = playersArray;

            return GetBufferFromJson(json);
        }

        public static List<byte> serializeResponse(ErrorResponse response)
        {
            JObject json = new JObject();
            json["ok"] = response.IsOk();
            json["message"] = response.GetMessage();

            return GetBufferFromJson(json);

        }

        public static List<byte> GetBufferFromJson(JObject json)
        {
            string jsonString = json.ToString();
            List<byte> buffer = BytesHelper.StringToBytes(jsonString);
            return buffer;
        }
    }
}
