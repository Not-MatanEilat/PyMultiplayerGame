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

        public ConnectToGameResponse(List<RectangleF> blocks) : base()
        {
            this.blocks = blocks;
        }

        public List<RectangleF> GetBlocks()
        {
            return blocks;
        }
    }
}
