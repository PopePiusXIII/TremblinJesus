using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Arrow
{
    private Transform arrowh;
    private float lenmax;
    private float valmax;

    public Arrow(Transform arrowT, float lengthMax, float valueMax)
    {
        arrowh = arrowT;
        lenmax = lengthMax;
        valmax = valueMax;
    }

    // Update is called once per frame
    public void Change(float length)
    {
        length = Mathf.Sign(length) * Mathf.Max(Mathf.Abs((length / valmax) * lenmax), 0);
        arrowh.transform.localScale = new Vector3(1f, length, 1f);

    }
}
