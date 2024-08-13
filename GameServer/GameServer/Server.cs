using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class Server
    {
        private Communicator communicator;
        public Server()
        {
            communicator = new Communicator();
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
