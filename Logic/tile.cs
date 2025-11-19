using UnityEngine: 


public class Tile : MonoBehaviour
{
    public int x, y;                 // Grid coords
    public string colorType;         // "Yellow", "Blue", "Green","Red"
    public bool isMatched = false;   // Flag for match clearing

    private Board board;

    void Start()
    {
        board = FindObjectOfType<Board>();
    }

    void OnMouseDown()
    {
        board.SelectTile(this);
    }
}