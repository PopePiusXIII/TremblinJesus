
using System;
using UnityEngine;

public class SimpleCarController : MonoBehaviour {

	public void GetInput()
	{
		m_horizontalInput = Input.GetAxis("Horizontal");
		m_verticalInput = Input.GetAxis("Vertical");
	}

	private void Steer()
	{
		m_steeringAngle = maxSteerAngle * m_horizontalInput;
		frontDriverW.steerAngle = m_steeringAngle;
		frontPassengerW.steerAngle = m_steeringAngle;
	}

	private void Accelerate()
	{
		frontDriverW.motorTorque =  Math.Max(0, m_verticalInput * motorForce);
		frontPassengerW.motorTorque =  Math.Max(0, m_verticalInput * motorForce);

		frontDriverW.brakeTorque = Math.Max(0, -m_verticalInput * motorForce);
		frontPassengerW.brakeTorque = Math.Max(0, -m_verticalInput * motorForce);
	}


	private void FixedUpdate()
	{
		GetInput();
		Steer();
		Accelerate();
	}

	private float m_horizontalInput;
	private float m_verticalInput;
	private float m_steeringAngle;

	public WheelCollider frontDriverW, frontPassengerW;
	public WheelCollider rearDriverW, rearPassengerW;
	public float maxSteerAngle = 30;
	public float motorForce = 500;
}
