using UntiyEngine;
using System.Collecctions;
using System.Collections.Generic;

publc class Board : MonoBehavior 
{   
    public int width = 8; 
    public int height = 8;
    public GameObject tilePrefab; 
    public Tile[,] allTiles; 
    public string[] colors;
}