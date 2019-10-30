// BSD 3-Clause License
//
// Copyright (c) 2018, The Regents of the University of California.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// * Redistributions of source code must retain the above copyright notice, this
//   list of conditions and the following disclaimer.
//
// * Redistributions in binary form must reproduce the above copyright notice,
//   this list of conditions and the following disclaimer in the documentation
//   and/or other materials provided with the distribution.
//
// * Neither the name of the copyright holder nor the names of its
//   contributors may be used to endorse or promote products derived from
//   this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#include "LinearRegression.h"

/*
 * constructor
 */
LinearRegression::LinearRegression() {
	GenerateWeight_random();
}

/*
 * pack: pack out to batch_data.
 */
char* LinearRegression::json(unsigned long timestamp, float *out, int out_size) {
  	StaticJsonBuffer<MSG_JSON_BUF_MAX_LEN> jsonBuffer;
	JsonObject& root = jsonBuffer.createObject();
	root["timestamp"] = timestamp;
  	JsonArray& array = root.createNestedArray("data");
    JsonArray& innerArray = jsonBuffer.createArray();
	for (int j = 0; j < out_size; ++j)
		innerArray.add(out[j]);
	array.add(innerArray);
  	root.printTo(buffer,sizeof(buffer));
  	return buffer;
}

/*
 * Run Linear Regression
 */
char* LinearRegression::Run(unsigned long timestamp, float lr_in[]) {
	if (lr_in_size > LR_IN || lr_out_size > LR_OUT)
		return NULL;
	// set lr_out array to zero
	memset(lr_out, 0, sizeof(lr_out));
  	// Run Linear Regression
  	for (int i = 0; i < lr_in_size; ++i)
  		for (int j = 0; j < lr_out_size; ++j)
  			lr_out[j] += lr_in[i] * weights[i][j];
  
  	// pack the result into send batch
	return json(timestamp, (float *)lr_out, lr_out_size);
}

/*
 * Randomly generate weights
 */
void LinearRegression::GenerateWeight_random() {
	for (int i = 0; i < LR_IN; ++i)
		for (int j = 0; j < LR_OUT; ++j)
			weights[i][j] = float(random(10000))/10000;
}