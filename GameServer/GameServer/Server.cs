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
        private Communicator communicator;
        private Game game;
        public Server()
        {
            Game game = new Game();
            communicator = new Communicator(game);
        }
        public void Start()
        {
            Thread communicatorThread = new Thread(communicator.HandleRequests);
            communicatorThread.Start();
            
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
