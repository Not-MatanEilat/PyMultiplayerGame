using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.GameRelated
{
    abstract class Sprite
    {
        protected int id;
        protected Vector2 position;
        protected float width;
        protected float height;

        private static int nextId = 1;

        public Sprite(Vector2 position, float width, float height)
        {
            this.id = GenerateId();
            this.position = position;
            this.width = width;
            this.height = height;
        }

        public RectangleF GetRectangle()
        {
            return new RectangleF(position.X, position.Y, width, height);
        }

        public void setRight(float right)
        {
            position.X = right - width;
        }

        public void setLeft(float left) 
        {
            position.X = left;
        }

        public void setTop(float top)
        {
            position.Y = top;
        }

        public void setBottom(float bottom)
        {
            position.Y = bottom - height;
        }

        public Vector2 GetPosition()
        {
            return position;
        }

        public virtual void SetPosition(Vector2 position)
        {
            this.position = position;
        }

        public static int GenerateId()
        {
            return nextId++;
        }
    }
}
