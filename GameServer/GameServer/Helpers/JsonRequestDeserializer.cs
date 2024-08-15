using GameServer.Requests;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Helpers
{
    internal class JsonRequestDeserializer
    {
        public static T DeserializeRequest<T>(List<byte> buffer) where T : IRequest
        {
            string stringBuffer = BytesHelper.BytesToString(buffer);
            T request = JObject.Parse(stringBuffer).ToObject<T>();
            return request;
        }
    }
}
