# SWAMI KARUPPASWAMI THUNNAI

import random
import sys
import struct
import socket
import string

class DomainNameGenerator:
    """
    This class is used to generate the Domain names
    """
    __query_count = 0
    __queries = []

    def __init__(self, query_count):
        self.__query_count = query_count
        self.build_queries()

    def build_queries(self):
        """
        Will generate random domain names for the specified count
        """
        alpha_numeric = tuple(string.ascii_lowercase+string.digits)
        for i in range(self.__query_count):
            domain = "".join([alpha_numeric[random.randrange(0, len(alpha_numeric))] for i in range(6)])
            self.__queries.append("www."+domain+".com")
    
    def get_domains(self):
        """
        :return: List of random domain names
        """
        return self.__queries

class StressDNS:
    """
    This class is actually used for DNS stress testing
    """
    __domain_names = []
    __dns_server = ""

    def __init__(self, dns_server, query_count):
        """
        :param dns_server:  The server to be tested
        :param query_count: The no of domain names
        """
        self.__dns_server = dns_server
        self.__domain_names = DomainNameGenerator(query_count).get_domains()
        self.encode_domain_names()
        self.send_queries()

    def encode_domain_names(self):
        """
        :return: Will encode all the alphaneumeric domain names to binary
        """
        index = 0
        for domain_name in self.__domain_names:
            self.__domain_names[index] = self.build_packet(domain_name)
            index+=1

    def build_packet(self, url):
        """
        :param url: The url which is to converted to it's binary form
        :return: The encoded the value of the url
        """
        packet = struct.pack(">H", random.randrange(1,65535))  # Query Ids
        packet += struct.pack(">H", 256)  # Flags
        packet += struct.pack(">H", 1)  # Questions
        packet += struct.pack(">H", 0)  # Answers
        packet += struct.pack(">H", 0)  # Authorities
        packet += struct.pack(">H", 0)  # Additional
        split_url = url.split(".")
        for part in split_url:
            packet += struct.pack("B", len(part))
            for byte in (part):
                packet += struct.pack("c", bytes(byte, 'utf-8'))
        packet += struct.pack("B", 0)  # End of String
        packet += struct.pack(">H", 1)  # Query Type
        packet += struct.pack(">H", 1)  # Query Class
        return packet


    def send_queries(self):
        """
        Description:
        ===========
        Domain Name Server a.k.a will be generally listening on Port No: 53
        in User Datagram Protocol which is  connectionless protocol so we use socket.SOCK_DGRAM.
        This method will send the queries to the DNS Server
        :return:
        """
        index = 0
        skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in self.__domain_names:
            skt.sendto(bytes(i), (str(self.__dns_server), 53))
            index = index+1
            sys.stdout.write("\r Sent "+ str(index))
            sys.stdout.flush()



if __name__=="__main__":
    limit = int(input('Enter the number of queries you wanna send: '))
    dns_server = input('Enter the DNS server to be stressed: ')
    StressDNS(dns_server, limit)

