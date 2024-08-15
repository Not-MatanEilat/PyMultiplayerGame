using GameServer.Exceptions;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.GameRelated
{
    internal class Game
    {
        private List<RectangleF> blocks;
        private List<Player> players;

        private const int targetUpdatesPerSecond = 60;
        private const int frameTime = 1000 / targetUpdatesPerSecond;

        public Game()
        {
            blocks = new List<RectangleF>();
            players = new List<Player>();

            blocks.Add(new RectangleF(0, 400, 50, 50));
            blocks.Add(new RectangleF(50, 400, 50, 50));
            blocks.Add(new RectangleF(100, 400, 50, 50));
            blocks.Add(new RectangleF(150, 400, 50, 50));
            blocks.Add(new RectangleF(200, 400, 50, 50));
            blocks.Add(new RectangleF(250, 400, 50, 50));
            blocks.Add(new RectangleF(300, 400, 50, 50));
        }

        public void mainLoop()
        {
            Stopwatch stopwatch = new Stopwatch();

            while (true)
            {
                stopwatch.Restart();









                stopwatch.Stop();

                int timeToSleep = frameTime - (int)stopwatch.ElapsedMilliseconds;

                if (timeToSleep > 0)
                {
                    System.Threading.Thread.Sleep(timeToSleep);
                }
            }
        }

        public List<RectangleF> GetBlocks()
        {
            return blocks;
        }

        public Player GetPlayer(string name)
        {
            foreach (Player player in players)
            {
                if (player.GetName() == name)
                {
                    return player;
                }
            }

            return null;
        }

        public void AddPlayer(Player player)
        {
            if (PlayerNameExists(player))
            {
                throw new GameException("Player with name " + player.GetName() + " already exists");
            }

            players.Add(player);

        }

        public bool PlayerNameExists(Player player)
        {
            
            foreach (Player p in players)
            {
                if (p.GetName() == player.GetName())
                {
                    return true;
                }
            }
            return false;
        }

        public void RemovePlayer(Player player)
        {
            players.Remove(player);
        }
    }
}
