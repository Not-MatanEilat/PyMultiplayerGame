using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using GameServer.GameRelated;
using GameServer.Helpers;
using GameServer.RequestHandlers;
using GameServer.Responses;

namespace GameServer
{
    enum RequestCodes : int
    {   
        ConnectToServer = 1,
        Error = 2,
        ConnectToGame = 3,
        Move = 4
    }
    internal class Communicator
    {
        public const int port = 6984;
        public const int maxRequestSize = 1024;

        private HandlerFactory handlerFactory;
        private Dictionary<Socket, IRequestHandler> clients;

        public Communicator(HandlerFactory handlerFactory)
        {
            clients = new Dictionary<Socket, IRequestHandler>();
            this.handlerFactory = handlerFactory;
        }
        public void HandleRequests()
        {
            TcpListener listener = SetupListener();

            while (true)
            {
                Console.WriteLine("Handling requests...");
                Socket socket = listener.AcceptSocket(); 

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
            CompleteConnection(clientSocket);

            try
            {
                // main client loop
                while (true)
                {
                    RequestInfo requestInfo = BytesHelper.GetRequestInfoFromSocket(clientSocket);
                    Console.WriteLine("Received request with code " + requestInfo.requestCode);
                    Console.WriteLine("Received request with buffer " + BytesHelper.BytesToString(requestInfo.buffer));
                    RequestResult requestResult = clients[clientSocket].HandleRequest(requestInfo);
                    if (requestResult.newHandler != null)
                    {
                        clients[clientSocket] = requestResult.newHandler;
                    }

                    BytesHelper.SendDataToSocketWithCode(clientSocket, requestResult.responseCode, requestResult.response);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("Client disconnected");
                clients[clientSocket].HandleDisconnect();
                clientSocket.Close();

            }

        }

        public void CompleteConnection(Socket clientSocket)
        {
            ConnectedToServerResponse response = new ConnectedToServerResponse();
            BytesHelper.SendDataToSocketWithCode(clientSocket, (int)RequestCodes.ConnectToServer, JsonResponseSerializer.serializeResponse(response));
            clients[clientSocket] = new ConnectToGameRequestHandler(handlerFactory.GetGame());

        }

        public Dictionary<Socket, IRequestHandler> GetClients()
        {
            return clients;
        }

        public List<Socket> GetClients<T>() where T : IRequestHandler
        {
            List<Socket> result = new List<Socket>();
            foreach (KeyValuePair<Socket, IRequestHandler> client in clients)
            {
                if (client.Value is T)
                {
                    result.Add(client.Key);
                }
            }

            return result;
        }
    }
}
