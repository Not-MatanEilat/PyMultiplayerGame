using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GameServer.GameRelated;

namespace GameServer
{
    internal class Server
    {
        HandlerFactory handlerFactory;
        public Server()
        {
            handlerFactory = new HandlerFactory();

        }
        public void Start()
        {
            Thread communicatorThread = new Thread(handlerFactory.GetCommunicator().HandleRequests);
            communicatorThread.Start();

            Thread gameThread = new Thread(handlerFactory.GetGame().mainLoop);
            gameThread.Start();

            String input = "";
            while (true)
            {
                input = Console.ReadLine();
                if (input == "exit")
                {
                    break;
                }
            }

            Console.WriteLine("Server is closing...");
        }
    }
}
