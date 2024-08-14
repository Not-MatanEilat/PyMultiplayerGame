using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer
{
    internal class Game
    {
        List<Rectangle> blocks;

        public Game() 
        {
            blocks = new List<Rectangle>();

            blocks.Add(new Rectangle(0, 400, 50, 50));
            blocks.Add(new Rectangle(50, 400, 50, 50));
            blocks.Add(new Rectangle(100, 400, 50, 50));
            blocks.Add(new Rectangle(150, 400, 50, 50));
            blocks.Add(new Rectangle(200, 400, 50, 50));
            blocks.Add(new Rectangle(250, 400, 50, 50));
            blocks.Add(new Rectangle(300, 400, 50, 50));
        }

        public List<Rectangle> GetBlocks()
        {
            return blocks;
        }
    }
}
