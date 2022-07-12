using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ForcesUI : MonoBehaviour
{
    public float fx;
    public Tire Tirex;
    TextMeshProUGUI text;

    void Start()
    {
        text = GetComponent<TextMeshProUGUI>();

    }

    // Update is called once per frame
    void Update()
    {
        text.text = "slipRatio:" + System.Math.Round(Tirex.slipRatio, 3).ToString() + "    Fx:" + Mathf.Round(Tirex.Fx).ToString();
    }
}
