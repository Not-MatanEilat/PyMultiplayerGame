using GameServer.GameRelated;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class HandlerFactory
    {
        private Communicator communicator;
        private Game game;

        public HandlerFactory()
        {
            communicator = new Communicator(this);
            game = new Game(this);
        }

        public Game GetGame()
        {
            return game;
        }

        public Communicator GetCommunicator()
        {
            return communicator;
        }
    }
}
