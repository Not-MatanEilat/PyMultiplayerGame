using GameServer.GameRelated;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Responses
{
    internal class ConnectToGameResponse : IResponse
    {
        private List<RectangleF> blocks;
        private List<Player> players;

        public ConnectToGameResponse(List<RectangleF> blocks, List<Player> players) : base()
        {
            this.blocks = blocks;
            this.players = players;
        }

        public List<RectangleF> GetBlocks()
        {
            return blocks;
        }

        public List<Player> GetPlayers()
        {
            return players;
        }
    }
}
