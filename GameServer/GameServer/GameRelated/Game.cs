﻿using GameServer.Exceptions;
using GameServer.RequestHandlers;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using GameServer.Responses;
using GameServer.Helpers;

namespace GameServer.GameRelated
{
    internal class Game
    {
        private List<RectangleF> blocks;
        private List<Player> players;

        private System.Timers.Timer updatePlayersTimer;
        private const int updatePlayersInterval = 50;

        private const int targetUpdatesPerSecond = 60;
        private const int frameTime = 1000 / targetUpdatesPerSecond;

        private HandlerFactory handlerFactory;

        public Game(HandlerFactory handlerFactory)
        {
            blocks = new List<RectangleF>();
            players = new List<Player>();

            blocks.Add(new RectangleF(-150, 400, 2500, 50));

            blocks.Add(new RectangleF(300, 300, 100, 100)); // First jump
            blocks.Add(new RectangleF(600, 200, 100, 100)); // Second jump
            blocks.Add(new RectangleF(900, 100, 100, 100)); // Third jump
            blocks.Add(new RectangleF(1200, 0, 100, 100));  // Fourth jump

            blocks.Add(new RectangleF(1500, -100, 400, 100)); // Final big platform

            this.handlerFactory = handlerFactory;

            SetupPlayersUpdateTimer();
        }

        private void SetupPlayersUpdateTimer()
        {
            updatePlayersTimer = new System.Timers.Timer(updatePlayersInterval);
            updatePlayersTimer.Elapsed += UpdatePlayers;
            updatePlayersTimer.Start();
        }

        private void UpdatePlayers(object sender, System.Timers.ElapsedEventArgs e)
        {
            List<Socket> playerClients = handlerFactory.GetCommunicator().GetClients<GameRequestHandler>();


            UpdatePlayersResponse response = new UpdatePlayersResponse(players);

            RequestResult result = new RequestResult();
            result.responseCode = (int)PacketsCodes.UpdatePlayers;
            result.response = JsonResponseSerializer.serializeResponse(response);

            Communicator communicator = handlerFactory.GetCommunicator();
            communicator.SendResultToClients(playerClients, result);
        }

        public void mainLoop()
        {
            Stopwatch stopwatch = new Stopwatch();

            while (true)
            {
                stopwatch.Restart();

                // Main game logic goes here



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

        public List<Player> GetPlayers()
        {
            return players;
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
            if (player.GetName() == "")
            {
                throw new GameException("Player name cannot be empty");
            }
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
