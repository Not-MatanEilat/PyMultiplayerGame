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
        private List<Rectangle> blocks;

        public ConnectToGameResponse(int id, List<Rectangle> blocks) : base(id)
        {
            this.blocks = blocks;
        }

        public List<Rectangle> GetBlocks()
        {
            return blocks;
        }
    }
}
