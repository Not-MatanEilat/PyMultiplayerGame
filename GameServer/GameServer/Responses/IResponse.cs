using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GameServer.Responses
{
    abstract class IResponse
    {
        private bool ok;

        public IResponse( bool ok = true)
        {
            this.ok = ok;
        }

        public bool IsOk()
        {
            return ok;
        }

        public void SetOk(bool ok)
        {
            this.ok = ok;
        }
    }
}
