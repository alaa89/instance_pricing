import unittest
import json
from instance_pricing.utils import func


class APITestCase(unittest.TestCase):

    def test_entry(self):
        expected = {'us-east-1': {'m3.2xlarge': '0.900', 'm3.xlarge': '0.450'},
                    'eu-west-1': {'m1.medium': '0.120', 'm1.small': '0.060', 'm1.large': '0.240'}}

        regions = [
            {
                "instanceTypes": [
                    {
                        "sizes": [
                            {
                                "size": "m3.xlarge",
                                "valueColumns": [
                                    {
                                        "name": "linux",
                                        "prices": {
                                            "USD": "0.450"
                                        }
                                    }
                                ]
                            },
                            {
                                "size": "m3.2xlarge",
                                "valueColumns": [
                                    {
                                        "name": "linux",
                                        "prices": {
                                            "USD": "0.900"
                                        }
                                    }
                                ]
                            }
                        ],
                        "type": "generalCurrentGen"
                    }
                ],
                "region": "us-east-1"
            },
            {
                "instanceTypes": [
                    {
                        "sizes": [
                            {
                                "size": "m1.small",
                                "valueColumns": [
                                    {
                                        "name": "linux",
                                        "prices": {
                                            "USD": "0.060"
                                        }
                                    }
                                ]
                            },
                            {
                                "size": "m1.medium",
                                "valueColumns": [
                                    {
                                        "name": "linux",
                                        "prices": {
                                            "USD": "0.120"
                                        }
                                    }
                                ]
                            },
                            {
                                "size": "m1.large",
                                "valueColumns": [
                                    {
                                        "name": "linux",
                                        "prices": {
                                            "USD": "0.240"
                                        }
                                    }
                                ]
                            }
                        ],
                        "type": "generalPreviousGen"
                    }
                ],
                "region": "eu-west-1"
            }
        ]
        result = func(regions)
        self.assertTrue(result == expected)


if __name__ == '__main__':
    unittest.main()
