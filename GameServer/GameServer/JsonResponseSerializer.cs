using GameServer.Responses;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class JsonResponseSerializer
    {
        public static List<byte> serializeResponse(ConnectToGameResponse response)
        {
            JObject json = new JObject();
            json["id"] = response.GetId();
            json["blocks"] = JArray.FromObject(response.GetBlocks());

            string jsonString = json.ToString();
            Console.WriteLine(jsonString);
            List<byte> buffer = BytesHelper.StringToBytes(jsonString);
            return buffer;
        }
    }
}
