using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class Communicator
    {
        public const int port = 6984;
        public const int maxRequestSize = 1024;

        private Dictionary<Socket, IRequestHandler> clients;

        public Communicator()
        {
            clients = new Dictionary<Socket, IRequestHandler>();
        }
        public void HandleRequests()
        {
            TcpListener listener = SetupListener();

            while (true)
            {
                Console.WriteLine("Handling requests...");
                Socket socket = listener.AcceptSocket();

                TestHandler testHandler = new TestHandler();
                clients[socket] = testHandler;  

                Thread clientThread = new Thread(() => acceptNewClient(socket));
                clientThread.Start();
            }
        }

        private TcpListener SetupListener()
        {
            IPAddress ipAddress = IPAddress.Parse("127.0.0.1");

            Console.WriteLine("Starting TCP listener...");

            TcpListener listener = new TcpListener(ipAddress, port);
            listener.Start();
            return listener;
        }

        private void acceptNewClient(Socket clientSocket)
        {

            // main client loop
            while (true)
            {
                RequestInfo requestInfo = BytesHelper.GetRequestInfoFromSocket(clientSocket);
                Console.WriteLine("Received request with code " + requestInfo.requestCode);
                Console.WriteLine("Received request with buffer " + BytesHelper.BytesToString(requestInfo.buffer));
                RequestResult requestResult = clients[clientSocket].handleRequest(requestInfo);

                BytesHelper.SendDataToSocket(clientSocket, requestResult.response);
            }


           

        }
    }
}
