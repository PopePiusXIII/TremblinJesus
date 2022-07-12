using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OneDRigidBody : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        transformBody = GetComponent<Transform>();
        rigidBody = GetComponent<Rigidbody>();

    }

    // Update is called once per frame
    void Update()
    {
        transformBody.position = (bodyA.position + bodyB.position) / 2;
    }

    private Transform transformBody;
    private Rigidbody rigidBody;
    public Transform bodyA;
    public Transform bodyB;
}
