﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class BytesHelper
    {
        public static List<byte> GetAmountFromSocket(Socket socket, int bytesAmount)
        {
            if (bytesAmount <= 0)
            {
                return new List<byte>();
            }

            byte[] buffer = new byte[bytesAmount];
            int size = socket.Receive(buffer);

            List<byte> result = new List<byte>(buffer);
            return result;
        }

        public static RequestInfo GetRequestInfoFromSocket(Socket socket)
        {
            List<byte> requestCodeBytes = GetAmountFromSocket(socket, 1);
            List<byte> bufferLengthBytes = GetAmountFromSocket(socket, 4);
            int requestCode = requestCodeBytes[0];
            bufferLengthBytes.Reverse();
            int bufferLength = BitConverter.ToInt32(bufferLengthBytes.ToArray(), 0);

            Console.WriteLine("Size: " + bufferLength);

            if (bufferLength > Communicator.maxRequestSize)
            {
                throw new Exception("Request too large");
            }

            List<byte> buffer = GetAmountFromSocket(socket, bufferLength);

            RequestInfo requestInfo = new RequestInfo();
            requestInfo.requestCode = requestCode;
            requestInfo.buffer = buffer;

            return requestInfo;
        }

        public static void SendDataToSocket(Socket socket, List<byte> data)
        {
            byte[] dataBytes = data.ToArray();
            socket.Send(dataBytes);
        }

        public static List<Byte> StringToBytes(string str)
        {
            return new List<byte>(Encoding.ASCII.GetBytes(str));
        }

        public static string BytesToString(List<byte> bytes)
        {
            return Encoding.ASCII.GetString(bytes.ToArray());
        }
    }
}
