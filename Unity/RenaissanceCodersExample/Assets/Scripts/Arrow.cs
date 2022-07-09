using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Arrow
{
    //Transform arrowT { get; set; }
    //Transform arrowR { get; set; }
    //float lengthMin { get; set; }
    //float lengthMax { get; set; }
    //float valueMin { get; set; }
    //float valueMax { get; set; }
    private Transform arrowh;
    private Rigidbody arrowi;
    private float lenmin;
    private float lenmax;
    private float valmin;
    private float valmax;

    private float length;

    public Arrow(Transform arrowT, Rigidbody arrowR, float lengthMin, float lengthMax, float valueMin, float valueMax)
    {
        arrowh = arrowT;
        arrowi = arrowR;
        lenmin = lengthMin;
        lenmax = lengthMax;
        valmin = valueMin;
        valmax = valueMax;
    }

    // Update is called once per frame
    public void Change()
    {
        length = (arrowi.velocity.magnitude / valmax) * lenmax;
        arrowh.transform.localScale = new Vector3(1f, length, 1f);

    }
}
