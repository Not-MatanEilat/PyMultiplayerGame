using GameServer.Exceptions;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.GameRelated
{
    internal class Player : Sprite
    {
        private Game game;
        private string name;

        private bool lockControls;
        
        public Player(string name, Game game) : base(new Vector2(50f, 50f), 50, 50)
        {
            this.game = game;

           this.name = name;

            lockControls = false;
            
        }


        public List<RectangleF> CurrentCollisions(List<RectangleF> blocks)
        {
            
                List<RectangleF> collisions = new List<RectangleF>();

                foreach (RectangleF block in blocks)
                {
                    if (block.IntersectsWith(GetRectangle()))
                    {
                        collisions.Add(block);
                    }
                }

                return collisions;
           
        }

        public override void SetPosition(Vector2 position)
        {
            if (lockControls)
            {
                throw new GameException("Player controls are locked");
            }
            if (CurrentCollisions(game.GetBlocks()).Capacity != 0)
            {
                throw new GameException("Player is colliding with a block");
            }

            base.SetPosition(position);
            
        }

        public string GetName()
        {
            return name;
        }
    }
}

