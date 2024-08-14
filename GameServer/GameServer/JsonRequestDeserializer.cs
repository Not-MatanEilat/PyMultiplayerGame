using GameServer.Requests;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class JsonRequestDeserializer
    {
        public static ConnectToGameRequest DesrializeRequest(List<Byte> buffer)
        {
            String stringBuffer = BytesHelper.BytesToString(buffer);
            ConnectToGameRequest request = JObject.Parse(stringBuffer).ToObject<ConnectToGameRequest>();
            return request;
        }
    }
}
