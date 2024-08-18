using GameServer.GameRelated;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Responses
{
    internal class UpdatePlayersResponse : IResponse
    {
        private List<Player> players;

        public UpdatePlayersResponse(List<Player> players) : base()
        {
            this.players = players;
        }

        public List<Player> GetPlayers()
        {
            return players;
        }
    }
}
